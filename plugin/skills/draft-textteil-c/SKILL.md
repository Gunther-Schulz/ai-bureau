---
name: draft-textteil-c
description: This skill should be used when the user asks to draft B-Plan Textliche Festsetzungen (the binding-rules part of the Satzung, Teil B Text). Triggered by phrases like "Entwurf Festsetzungen", "Festsetzungen schreiben", "draft Textliche Festsetzungen", "Satzungstext aufsetzen", "Teil B Text". Phase A entry skill for the second canonical B-Plan doctype.
version: 0.1.0
license: MIT
---

# draft-textteil-c

Specialist skill for drafting B-Plan Textliche Festsetzungen — the
binding-rules document attached to the Satzung as "Teil B Text".
Different shape from Begründung: single article doc with infinite-page
geometry, sans-serif body, numbered enumerate of binding rules,
13-entry Verfahrensvermerke sequence.

## Load this now

Read `PROCEDURE.md` from this skill's directory for the rule-by-rule
workflow.

While operating, hold these references loaded:

- `<repo>/memory/universal/style/style-spec.md` — Doctype B spec
  (article + pdflatex + sans-serif + infinite-page).
- `<repo>/memory/universal/conventions/korrektur-rules.md` — writing
  conventions.
- `<repo>/memory/universal/verfahren/bauleitplanung-phasen.md` —
  Verfahrensvermerke sequence + phase context.
- `<repo>/plugin/skills/validate-checklist/references/checklists/
  b-plan-festsetzungen.md` — required structure.

## When invoked

By orchestrator (Phase A entry) or direct user request. Usually
follows draft-textteil-b for the same project; the two are produced
as a pair per B-Plan.

Inputs:

- **Project** — bound; state.md available.
- **Drafted Begründung** (when available) — content cross-references.
- **Source materials** — same as Begründung scope; especially: site
  data, technical specs, artenschutzrechtliche Maßgaben.
- **Verfahren type** — same as Begründung.
- **B-Plan name + number** — from state.md / Projektdaten.

## Behavior

1. **Verify Begründung-state**: ideally drafted first because rules
   in Festsetzungen mirror narrative arguments. If Begründung
   absent/incomplete, surface; allow user to draft in parallel
   with caveat that consistency-check happens at end.

2. **Scaffold the LaTeX project structure** if not present:
   - Call `scaffold_project(doctype="b-plan-festsetzungen",
     target_root=<project>/<doctype-subfolder>/)`.
     The tool resolves the skeleton from the app's
     `templates/skeletons/b-plan-festsetzungen/` (default) or from
     the office's `templates.doctype_overrides[b-plan-festsetzungen]`
     if set.
   - Instantiate `Projektdaten.tex` consistently with Begründung's
     Projektdaten.tex (same Gemeinde, BPlanName, etc. — divergence
     is a bug).
   - `git init` LaTeX subfolder if Overleaf sync wanted.

3. **Compose the Satzung header**:
   - `\textbf{Satzung der Gemeinde \Gemeinde{} über den \BPlan{}}`
   - Präambel (recites BauGB §10 + LBauO M-V refs + Beschluss-
     fassung — verify-citations needs to confirm amendments are
     current).

4. **Compose Teil A reference**: heading `\subsection*{Teil A:
   Planzeichnung i. M. 1 : 2.000}` — placeholder; the actual
   Planzeichnung is separate.

5. **Compose Teil B Text — numbered rules**:
   - Required rules per checklist:
     1. Art der baulichen Nutzung (§9 Abs.1 BauGB)
     2. Maß der baulichen Nutzung (§9 (1) Nr.1)
     3. Flächen + Maßnahmen Schutz/Pflege/Entwicklung (§9 Abs.1 Nr.20)
     4. Artenschutzrechtliche Festsetzungen (if §44 BNatSchG triggered)
     5. Örtliche Bauvorschriften (§86 Abs.3 LBauO M-V)
   - Each rule with nested 1.1, 1.2, ... structure.
   - Project-specific values from state.md.

6. **Compose Verfahrensvermerke**: 13-entry sequence per
   bauleitplanung-phasen.md. Tabbing-blocks per Vermerk with Ort,
   Datum (placeholder ................), Siegel, Bürgermeister-Name.

7. **Compose Hinweis (Denkmalschutz)**: standard §11 DSchG M-V
   boilerplate.

8. **Compose centered title-block**: SATZUNG DER GEMEINDE / <name>
   / ÜBER DEN / <BPlan-typ-name>.

9. **Compose Rechtsgrundlagen** (last section): bullet list of
   cited laws with current amendment dates. Cross-checked by
   verify-citations.

10. **Compile via latexmk**. Address errors. Verify output is one
    PDF page (paperheight=4000pt; if overflow, surface).

11. **Cross-consistency check** with Begründung:
    - Same Gemeinde, BPlan, BPlanTyp, GeltungsbereichHa values.
    - Festsetzungen rules align with Begründung argumentation.
    - Surface any divergence.

12. **Hand off to review-draft** for Phase B.

## Output

- LaTeX project at `<project>/B-Plan/Festsetzungen/` with master
  file, preamble, Projektdaten.tex.
- Compiled PDF (single page, ~141cm long).
- `_ai/decisions.md` entries for rule-content choices.
- `_ai/module-decisions.md` entries for optional rules
  (Artenschutzrechtliche, Wasserwirtschaftliche, etc.).

## Edge cases

- **Begründung not yet drafted**: surface, ask whether to draft in
  parallel or wait. Festsetzungen depends on Begründung's
  argumentation for consistency.
- **Existing rules in repository (rare for new project)**: ask
  whether to replace or build on.
- **Verfahren-type Genehmigungspflicht uncertain** (e.g. §10 Abs.2
  applicability): query user; affects Verfahrensvermerk #11
  (Genehmigung HVB).
- **Bürgermeister-Name unknown**: write `<Bürgermeister-Name>`
  placeholder; flag in module-decisions.md for user resolution.
- **Bekanntmachungsblatt name unknown**: write `<Bekanntmachungs-
  blatt>`; same.

## Tools used (when MCP backend lands)

- `search_corpus(filter={doctype: b-plan-festsetzungen})` — past
  Festsetzungen for similar Vorhaben.
- `list_bausteine`, `get_baustein` — Festsetzungs-baustein patterns.
- `scaffold_project`, `compile_latex` — same as B.

Until backend lands: filesystem reads + Bash for latexmk.
