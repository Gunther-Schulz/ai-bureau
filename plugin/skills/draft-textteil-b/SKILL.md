---
name: draft-textteil-b
description: This skill should be used when the user asks to draft a B-Plan Begründung (Textteil B) from project source materials. Triggered by phrases like "Entwurf Begründung", "Begründung schreiben", "draft Begründung", "Textteil B aufsetzen", "neue Begründung", "Vorentwurf Begründung". Phase A entry skill — orchestrator routes here when a project requires fresh Begründung drafting.
version: 0.3.0
license: MIT
mcp_tools_required: [list_skeletons, list_bausteine, search_corpus, compile_latex]
mcp_tools_optional: [list_doctypes_manifests, list_reference_manifests, get_baustein, search_inputs, ingest_project_inputs, scaffold_project, find_bausteine_by_reference, read_corpus_file]
fallback_when_mcp_absent: "warn user; degrade to filesystem reads + Bash latexmk for compile. Bausteine retrieval via Glob; corpus search via Grep over references_root + projects_root. Recall worse without semantic search."
summary: Drafts a B-Plan Begründung (Textteil B) from project source materials. Phase A entry skill.
routing_mode: direct
triggers:
  - {phrase: "Entwurf Begründung", lang: de}
  - {phrase: "Begründung schreiben", lang: de}
  - {phrase: "draft Begründung", lang: en}
  - {phrase: "Textteil B aufsetzen", lang: de}
  - {phrase: "neue Begründung", lang: de}
  - {phrase: "Vorentwurf Begründung", lang: de}
handoffs: [review-draft]
phase_role: phase_a_entry
---

# draft-textteil-b

Specialist skill for drafting a B-Plan Begründung from project
source materials. Phase A entry per the orchestrator's three-phase
model (draft → review → finalize). Produces a compileable LaTeX
document that goes through Phase B review next.

## Load this now

Read `PROCEDURE.md` from this skill's directory for the detailed
section-by-section workflow.

While operating, hold these references loaded:

- `<repo>/memory/universal/style/style-spec.md` — universal
  structural domain (KOMA scrreprt, German conventions).
- `<repo>/memory/universal/conventions/korrektur-rules.md` —
  office writing conventions.
- `<repo>/memory/universal/verfahren/bauleitplanung-phasen.md` —
  phase context for Stand-des-Aufstellungsverfahrens-section.
- `<repo>/plugin/skills/validate-checklist/references/checklists/b-plan-begruendung.md`
  — required-sections list.

For doctype + skeleton resolution, call
`list_doctypes_manifests()` (returns layered universal +
per-active-domain doctype registry) and
`list_skeletons("b-plan-begruendung")` (returns the layered
skeleton dirs: universal layer + per-active-domain overlays).

Cross-cutting memory docs touched during drafting (e.g. anything
that names a law) should declare their citations in
`references_used[]` frontmatter so research-references can
flag them on amendment.

## When invoked

By orchestrator (Phase A entry) or direct user request. Inputs:

- **Project** — bound or proposed; loads state.md if bound.
- **Source materials** — `inputs/` content (briefing, surveys,
  drone scans, regulatory inputs, prior Stellungnahmen).
- **Doctype focus** — confirmed `b-plan-begruendung` (not c, not
  Umweltbericht).
- **Verfahren type** — Regelverfahren / vereinfachtes (§13) /
  beschleunigtes (§13a) / vorhabensbezogen (§12). Affects
  sections + content.

## Behavior

1. **Bind project** if not already bound (delegate to
   orchestrator's binding flow + survey-project).

2. **Index project inputs** if not indexed: call
   `ingest_project_inputs(project, paths=...)`. Document this
   in `_ai/decisions.md`.

3. **Search corpus for similar context**:
   - `search_corpus(query=..., filter={doctype:
     b-plan-begruendung})` for similar past projects (same
     client, same Standort-typ, same Verfahren).
   - List candidates to user as reference material — user picks
     1-3 for active reference during drafting.

4. **Load applicable bausteine** via scope-aware enumeration:
   - `list_bausteine(scope="universal")` — universal patterns
     (cross-bureau).
   - `list_bausteine(scope="domain", scope_key=<X>)` for each
     active domain (e.g. `Naturschutz`, `PV-FFA`, `Wind` — not
     legacy lowercase tags).
   - `list_bausteine(scope="state", scope_key=<state>)` for
     state-specific patterns (e.g. `MV`).
   - `list_bausteine(scope="project", project_root=<path>)` for
     project-scope bausteine PLUS any
     `cross_project_visible: true` bausteine from other
     projects in the same office.
   - For solar/PV projects: include Naturschutz-domain bausteine
     where §44/§45 BNatSchG come into play.

5. **Scaffold the LaTeX project structure** if not present via
   layered skeleton composition:
   - Call
     `setup_project(name=..., doctypes=["b-plan-begruendung"],
     target_root=<project>/<doctype-subfolder>/)`.
     The MCP tool resolves the layered skeleton via
     `list_skeletons("b-plan-begruendung")` — copies the
     universal layer first, then overlays per-active-domain
     skeletons for the office's `scope.domains`. Office's
     `templates.doctype_overrides[b-plan-begruendung]` (if set
     in office-config) takes precedence over the layered
     default.
   - Instantiate `Projektdaten.tex` with project metadata from
     state.md.
   - `git init` the LaTeX subfolder if user wants Overleaf sync.

6. **Draft section-by-section** per PROCEDURE.md. Each section:
   - Identify required content from canonical-section list +
     doctype manifest entry's `references_required[]`.
   - Pull source inputs relevant to section
     (`search_inputs(query, project)`).
   - Search corpus for similar section in past projects.
   - Apply applicable bausteine (cite via History; record
     successful_use eventually).
   - Draft prose adhering to korrektur-rules.
   - Surface to user for feedback before moving to next
     section.

7. **Module decisions** — when including/excluding optional
   sections (Brandschutz, Denkmalschutz, etc.), log to
   `_ai/module-decisions.md` per orchestrator Checkpoint 6.3.

8. **Compile via `compile_latex(project_path)`** after each
   meaningful checkpoint. Address build errors before moving
   forward (orchestrator Compile Gate 4.1).

9. **Hand off to review-draft** when full draft is compileable
   — orchestrator transitions Phase A → Phase B.

## Output

Per section:
- Drafted .tex content written to
  `<project>/B-Plan/Begründung/Textbausteine/<section>.tex`.
- One-line summary of what's drafted + sources used (inputs
  cited, bausteine applied, corpus refs).
- Compile status after section integration.

End-of-draft:
- Full Begründung compiled to PDF.
- `_ai/decisions.md` entries for major argumentation choices.
- `_ai/module-decisions.md` entries for optional-section
  choices.
- Orchestrator-handoff to Phase B review.

## Edge cases

- **Source material insufficient for a required section**:
  surface gap; ask user for missing input or authorize "minimal
  default" language.
- **Verfahren-type uncertain**: refuse to draft phase-dependent
  sections (Stand des Aufstellungsverfahrens) until decided.
- **Existing draft conflicts**: if Textbausteine/<section>.tex
  exists with content, ask whether to replace, append, or skip.
  Don't silently overwrite.
- **Corpus search yields no similar past project**: surface;
  let user authorize "from scratch" or postpone until first
  comparable project exists.
- **Domain skeleton overlay conflicts with universal**: per
  layered skeleton composition, domain overlays add files
  on top of universal. If a domain-specific file would
  replace a universal file, surface as conflict + ask user.

## Tools used

- `list_skeletons(doctype)` (MCP, required) — layered skeleton
  resolution per scope.
- `list_bausteine(scope?, scope_key?, project_root?)` (MCP,
  required) — scope-aware baustein enumeration.
- `search_corpus(query, filter)` (MCP, required) — past
  projects + reference grounding.
- `compile_latex(project_path)` (MCP, required) — build cycles.
- `list_doctypes_manifests(scope_filter=true)` (MCP, optional)
  — required-sections + references_required per doctype entry.
- `list_reference_manifests(scope_filter=true)` (MCP, optional)
  — manifest set for citation cross-reference.
- `get_baustein(name, scope?, scope_key?)` (MCP, optional) —
  fetch full baustein content for active reference.
- `search_inputs(project, query)` (MCP, optional) —
  per-project input search.
- `ingest_project_inputs(project, paths)` (MCP, optional) —
  first-time ingestion of project inputs.
- `scaffold_project(name, doctype, target_root)` (MCP,
  optional) — alternate path if setup_project not used.
- `find_bausteine_by_reference(law?, paragraph?, ruling?,
  leitfaden?)` (MCP, optional) — find related patterns.
- `read_corpus_file(path)` (MCP, optional) — full reference
  read when needed.

When MCP backend unreachable: fall back to filesystem reads +
`Bash latexmk -pdf` for compile. Bausteine retrieval via
`Glob` over `memory/bausteine/{universal,domain/<X>,state/<X>}/`;
corpus search via `Grep` over `references_root` and
`projects_root`. Recall worse without semantic search; warn
user about degraded mode.
