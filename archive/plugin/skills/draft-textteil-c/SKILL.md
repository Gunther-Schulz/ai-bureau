---
name: draft-textteil-c
description: This skill should be used when the user asks to draft B-Plan Textliche Festsetzungen (the binding-rules part of the Satzung, Teil B Text). Triggered by phrases like "Entwurf Festsetzungen", "Festsetzungen schreiben", "draft Textliche Festsetzungen", "Satzungstext aufsetzen", "Teil B Text". Phase A entry skill for the second canonical B-Plan doctype.
version: 0.5.0
license: MIT
mcp_tools_required: [list_skeletons, list_bausteine, search_corpus, compile_latex, get_project_state, update_project_state]
mcp_tools_optional: [list_doctypes_manifests, list_reference_manifests, get_baustein, scaffold_project, find_bausteine_by_reference]
fallback_when_mcp_absent: "without get/update_project_state the skill cannot proceed (state.md is gate-only per ARCHITECTURE meta-rule 4 fail-closed corollary; surface 'MCP unreachable; restart backend' and stop). When the gate is up but optional MCP tools are unavailable: latexmk via Bash for compile; corpus search via Grep (recall worse without semantic search). Bausteine retrieval requires the gate (frontmatter contract — also fail-closed)."
summary: Drafts B-Plan Textliche Festsetzungen (Teil B Text) — the binding-rules section. Phase A entry skill.
routing_mode: direct
triggers:
  - draft Festsetzungen      # B-Plan Teil B Text; German technical anchor
  - Satzungstext aufsetzen
  - draft Textliche Festsetzungen
handoffs: [review-draft]
phase_role: phase_a_entry
---

# draft-textteil-c

Specialist skill for drafting B-Plan Textliche Festsetzungen — the
binding-rules document attached to the Satzung as "Teil B Text".
Different shape from Begründung: single article doc with
infinite-page geometry, sans-serif body, numbered enumerate of
binding rules, 13-entry Verfahrensvermerke sequence.

## Load this now

Read `PROCEDURE.md` from this skill's directory for the rule-by-rule
workflow.

While operating, hold these references loaded:

- `<repo>/memory/universal/style/style-spec.md` — Doctype B
  spec (article + pdflatex + sans-serif + infinite-page).
- `<repo>/memory/universal/conventions/korrektur-rules.md` —
  writing conventions.
- `<repo>/memory/universal/verfahren/bauleitplanung-phasen.md` —
  Verfahrensvermerke sequence + phase context.
- `<repo>/plugin/skills/validate-checklist/references/checklists/b-plan-festsetzungen.md`
  — required structure.

For doctype + skeleton resolution, call
`list_doctypes_manifests()` and
`list_skeletons("b-plan-festsetzungen")` (returns layered
universal + per-active-domain overlays).

## When invoked

By orchestrator (Phase A entry) or direct user request. Usually
follows draft-textteil-b for the same project; the two are
produced as a pair per B-Plan.

Inputs:

- **Project** — bound; project state available via `get_project_state(project)` (never Read state.md directly per ARCHITECTURE meta-rule 4).
- **Drafted Begründung** (when available) — content cross-references.
- **Source materials** — same as Begründung scope; especially:
  site data, technical specs, artenschutzrechtliche Maßgaben.
- **Verfahren type** — same as Begründung.
- **B-Plan name + number** — from `get_project_state(project).state` / Projektdaten.

## Behavior

1. **Verify Begründung-state**: ideally drafted first because
   rules in Festsetzungen mirror narrative arguments. If
   Begründung absent/incomplete, surface; allow user to draft
   in parallel with caveat that consistency-check happens at
   end.

2. **Scaffold the LaTeX project structure** if not present via
   layered skeleton composition:
   - Call
     `setup_project(name=..., doctypes=["b-plan-festsetzungen"],
     target_root=<project>/<doctype-subfolder>/)`.
     The MCP tool resolves the layered skeleton via
     `list_skeletons("b-plan-festsetzungen")` — universal
     layer + per-active-domain overlays from the office's
     `scope.domains`.
   - Instantiate `Projektdaten.tex` consistently with
     Begründung's Projektdaten.tex (same Gemeinde, BPlanName,
     etc. — divergence is a bug).
   - `git init` LaTeX subfolder if Overleaf sync wanted.

3. **Compose the Satzung header**:
   - `\textbf{Satzung der Gemeinde \Gemeinde{} über den \BPlan{}}`
   - Präambel (recites BauGB §10 + LBauO M-V refs +
     Beschlussfassung — verify-citations needs to confirm
     amendments are current).

4. **Compose Teil A reference**: heading `\subsection*{Teil A:
   Planzeichnung i. M. 1 : 2.000}` — placeholder; the actual
   Planzeichnung is separate.

5. **Compose Teil B Text — numbered rules**:
   - Required rules per checklist:
     1. Art der baulichen Nutzung (§9 Abs.1 BauGB)
     2. Maß der baulichen Nutzung (§9 (1) Nr.1)
     3. Flächen + Maßnahmen Schutz/Pflege/Entwicklung (§9
        Abs.1 Nr.20)
     4. Artenschutzrechtliche Festsetzungen (if §44 BNatSchG
        triggered)
     5. Örtliche Bauvorschriften (§86 Abs.3 LBauO M-V)
   - Each rule with nested 1.1, 1.2, ... structure.
   - Project-specific values from `get_project_state(project).state` (gate-only).
   - Apply applicable bausteine via `list_bausteine` per
     scope (esp. `domain/Naturschutz` for artenschutzrechtliche
     Festsetzungen patterns; `state/MV` for state-specific
     interpretations).

6. **Compose Verfahrensvermerke**: 13-entry sequence per
   bauleitplanung-phasen.md. Tabbing-blocks per Vermerk with
   Ort, Datum (placeholder ................), Siegel,
   Bürgermeister-Name.

7. **Compose Hinweis (Denkmalschutz)**: standard §11 DSchG M-V
   boilerplate (state-specific; sourced from state/MV
   bausteine if available).

8. **Compose centered title-block**: SATZUNG DER GEMEINDE /
   <name> / ÜBER DEN / <BPlan-typ-name>.

9. **Compose Rechtsgrundlagen** (last section): bullet list of
   cited laws with current amendment dates. Cross-checked by
   verify-citations.

10. **Compile via `compile_latex(project_path)`**. Address
    errors. Verify output is one PDF page (paperheight=4000pt;
    if overflow, surface).

11. **Cross-consistency check** with Begründung:
    - Same Gemeinde, BPlan, BPlanTyp, GeltungsbereichHa values.
    - Festsetzungen rules align with Begründung argumentation.
    - Surface any divergence.

12. **Hand off to review-draft** for Phase B.

## Output

- LaTeX project at `<project>/B-Plan/Festsetzungen/` with
  master file, preamble, Projektdaten.tex.
- Compiled PDF (single page, ~141cm long).
- `_ai/decisions.md` entries for rule-content choices.
- `_ai/module-decisions.md` entries for optional rules
  (Artenschutzrechtliche, Wasserwirtschaftliche, etc.).

## Edge cases

- **Begründung not yet drafted**: surface, ask whether to draft
  in parallel or wait. Festsetzungen depends on Begründung's
  argumentation for consistency.
- **Existing rules in repository (rare for new project)**: ask
  whether to replace or build on.
- **Verfahren-type Genehmigungspflicht uncertain** (e.g. §10
  Abs.2 applicability): query user; affects Verfahrensvermerk
  #11 (Genehmigung HVB).
- **Bürgermeister-Name unknown**: write `<Bürgermeister-Name>`
  placeholder; flag in module-decisions.md for user resolution.
- **Bekanntmachungsblatt name unknown**: write
  `<Bekanntmachungs-blatt>`; same.
- **State scope key not in office's scope** (e.g. project in
  BB but office's scope.states only has MV): the LBauO + DSchG
  references won't resolve from `state/MV` bausteine. Warn
  user; suggest adding the project's Bundesland to office's
  scope (via setup-office reconcile) OR sourcing those rules
  manually from BB-specific references.

## Tools used

- `list_skeletons(doctype)` (MCP, required) — layered skeleton
  resolution.
- `list_bausteine(scope?, scope_key?)` (MCP, required) —
  scope-aware baustein enumeration (esp.
  `domain/Naturschutz` + `state/<X>`).
- `search_corpus(query, filter)` (MCP, required) — past
  Festsetzungen for similar Vorhaben.
- `compile_latex(project_path)` (MCP, required) — build cycles.
- `list_doctypes_manifests(scope_filter=true)` (MCP, optional)
  — required-rules per doctype entry.
- `list_reference_manifests(scope_filter=true)` (MCP, optional)
  — for citation cross-reference (especially state-specific
  laws like LBauO M-V).
- `get_baustein(name, scope?, scope_key?)` (MCP, optional) —
  fetch Festsetzungs-baustein patterns.
- `scaffold_project(name, doctype, target_root)` (MCP,
  optional) — alternate path if setup_project not used.
- `find_bausteine_by_reference(law?, paragraph?)` (MCP,
  optional) — locate bausteine that share legal references.

When MCP backend unreachable: fall back to filesystem reads +
`Bash latexmk` for compile. Warn user about degraded mode.
